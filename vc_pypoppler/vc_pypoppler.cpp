/*
 * Copyright (C) 2012, Pierre Marchand <pierre@oep-h.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street - Fifth Floor, Boston, MA 02110-1301, USA.
 */



#include <boost/python.hpp>
#include <boost/smart_ptr.hpp>


#include <poppler-document.h>
#include <poppler-page.h>
#include <poppler-page-renderer.h>
#include <poppler-image.h>


typedef boost::shared_ptr<poppler::document> DocumentPtr;
typedef boost::shared_ptr<poppler::page> PagePtr;


class DocumentLoader
{
public:
	DocumentPtr from_file(const std::string& fn)
	{
		return DocumentPtr(poppler::document::load_from_file(fn));
	}

	DocumentPtr from_data(const std::string& data)
	{
		poppler::byte_array *b_data(new poppler::byte_array(data.begin(), data.end()));
		
 		poppler::document* doc(poppler::document::load_from_data(b_data));
		if(!doc)
		{
			std::cerr<<"Couldn't create a Poppler document"<<std::endl;
			return DocumentPtr();
		}
		DocumentPtr ret(doc);
		return ret;
	}
};


PagePtr page(DocumentPtr doc, int idx)
{
	return PagePtr(doc->create_page(idx));
}

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(render_page_overloads, poppler::page_renderer::render_page, 1, 8);

std::string image_data(poppler::image* image)
{
	return std::string(image->const_data(), image->bytes_per_row() * image->height());
}

BOOST_PYTHON_MODULE(vc_poppler)
{
	using namespace boost::python;
	
	/// global
	enum_<poppler::rotation_enum>("rotation")
		.value("rotate_0", poppler::rotate_0)
		.value("rotate_90", poppler::rotate_90)
		.value("rotate_180", poppler::rotate_180)
		.value("rotate_270", poppler::rotate_270)
	;
	
	/// document
	class_<DocumentLoader>("Loader")
		.def("from_file", &DocumentLoader::from_file)
		.def("from_data", &DocumentLoader::from_data)
	;
	
// 	PagePtr (poppler::document::*bp_create_page_)(int) const =&poppler::document::create_page;
	
	class_<poppler::document, DocumentPtr, boost::noncopyable>("Document", no_init)
// 		.def("load_from_file", load_from_file, return_value_policy<manage_new_object>())
// 		.def("load_from_data", load_from_data, return_value_policy<manage_new_object>())
		.def("pages", &poppler::document::pages)
		.def("page", page)
	;
    
	enum_<poppler::document::page_mode_enum>("page_mode")
		.value("use_none", poppler::document::use_none)
		.value("use_outlines", poppler::document::use_outlines)
		.value("use_thumbs", poppler::document::use_thumbs)
		.value("fullscreen", poppler::document::fullscreen)
		.value("use_oc", poppler::document::use_oc)
		.value("use_attach", poppler::document::use_attach)
	;
	
	enum_<poppler::document::page_layout_enum>("page_layout")
		.value("no_layout", poppler::document::no_layout)
		.value("single_page", poppler::document::single_page)
		.value("one_column", poppler::document::one_column)
		.value("two_column_left", poppler::document::two_column_left)
		.value("two_column_right", poppler::document::two_column_right)
		.value("two_page_left", poppler::document::two_page_left)
		.value("two_page_right", poppler::document::two_page_right)
	;
	
	/// page
	class_<poppler::page, PagePtr, boost::noncopyable>("Page", no_init);
	
	
	/// page_renderer
	
	class_<poppler::page_renderer, boost::noncopyable>("PageRenderer")
		.def("render_page", &poppler::page_renderer::render_page, 
		     render_page_overloads(args("page", "xres","yres", "x", "y", "w", "h", "rotate"), "Render the given page and return an Image"))
		.def("set_render_hint", &poppler::page_renderer::set_render_hint)
	;
	
	enum_<poppler::page_renderer::render_hint>("render_hint")
		.value("antialiasing", poppler::page_renderer::antialiasing)
		.value("text_antialiasing", poppler::page_renderer::text_antialiasing)
		.value("text_hinting", poppler::page_renderer::text_hinting)
	;
	
	/// image
	class_<poppler::image>("Image")
		.def("data", image_data)
		.def("format", &poppler::image::format)
		.def("width", &poppler::image::width)
		.def("height", &poppler::image::height)
		.def("bytes_per_row", &poppler::image::bytes_per_row)
	;
	
	enum_<poppler::image::format_enum>("format_enum")
		.value("format_invalid", poppler::image::format_invalid)
		.value("format_mono", poppler::image::format_mono)
		.value("format_rgb24", poppler::image::format_rgb24)
		.value("format_argb32", poppler::image::format_argb32)
	;
}


