# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Website Portfolio",
    "author" : "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "info@softhealer.com",    
    "category": "Website",
    "description": """Portfolio is a fully responsive module that display your company or personal portfolio/Gallery items. From admin panel you can easily add your portfolio items. Awesome Filterable Portfolio allows you to create, manage and publish a very modern and outstanding filterable portfolio that can be filtered using smooth animations and cool image hover effects.
                    """,    
    "summary": """ Portfolio is a fully responsive module that display your company or personal portfolio/Gallery items.
                    """,    
    "version":"12.0.1",
    "depends" : ["base","website"],
    "application" : True,
    "data" : [
        
            "security/ir.model.access.csv",            
            "views/website_backend_portfolio.xml",             
            "views/sh_website_portfolio_template.xml", 
            "data/sh_website_portfolio_data.xml",            
            
            ],            
    "images": ["static/description/background.png",],              
    "auto_install":False,
    "installable" : True,
    "price": 25,
    "currency": "EUR"   
}