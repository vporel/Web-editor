# -*- coding:utf-8 -*-

"""
    The languages are HTML, CSS, JAVASCRIPT, PHP
"""
#Structure

"""
    nom_langage:{
        extensions,
        mots_cles,
        coloration:(mots à colorier)
    }
"""

LANGUAGES = {

    ## Partie du langage HTML

    "HTML":{
        "exts" : ["html", "htm"],
        "keywords" : {
            "tags":[
                "!Doctype HTML","!Doctype", "html", "head", "body", "header", "article", "aside", "footer", "nav",
                "title", "meta", "link", "ul", "ol", "li","script","style", "div", "span", "section",
                "fieldset", "legend","br", "hr",
                "table", "caption", "thead", "tbody", "tfoot", "tr", "td", "th",
                "h1", "h2", "h3", "h4", "h5", "h6", "p", "b", "strong", "i", "u", "em", "pre",
                "form", "input", "button", "textarea",
                "img", "audio", "video", "source", "details", "summary", "menu", "menuitem",
                "a"
            ],
            "attributes": [
                "lang", "style", "charset", "name", "href", "rel", "type", "align",
                "bgcolor", "class", "id","contextmenu",
                "cellspacing", "cellpadding", "border", "color",
                "src", "alt", "width", "height",
                "enctype", "method", "action", "placeholder", "value", "max-length", "max", "min"
            ]
        },
        "coloration" : ["Balises", "Balises inconnues", "Attributs", "Attributs inconnus", "Textes attributs", "Commentaires"]
    },

    ##Langage css

    "CSS":{
        "exts" : ["css", "scss"],
        "keywords" : {
            "properties": [
                "font", "font-color", "font-style", "font-weight", "font-family", "font-size",
                "background", "background-color", "background-attachment", "background-image", "background-position",
                "background-size", "background-origin",
                "text-align","color", "text-underline",
                "position", "top", "bottom", "left", "right", "clear", "display",
                "flex-flow", "fle-direction", "align-items", "justify-content", "flex-grow", "flex-shrink",
                "order",
                "margin", "padding", "margin-top", "margin-bottom", "margin-left", "margin-right", "padding-top",
                "padding-bottom", "padding-left", "padding-right",
                "border", "border-width", "border-style", "border-color", "border-radius",
                "border-top-width", "border-top-style", "border-top-color",
                "border-bottom-width", "border-bottom-style", "border-bottom-color",
                "border-left-width", "border-left-style", "border-left-color",
                "border-right-width", "border-right-style", "border-right-color",
                "width", "height", "vertical-align", "behavior",
                "box-shadow", "text-shadow", "transform","animation", "transition", "filter",

                #spéciaux
                "@keyframes", "@media", "@import", "@charset"
            ],
            "values":[
                "none", "block", "inline", "inline-block", "flex",
                "row", "wrap", "nowrap", "center", "justify",
                "relative", "absolute", "fixed", "static",
                "sans-serif", "calibri", "verdana", "arial",
                "italic", "bold", "normal",
                "solid", "ridge", "double",
                "rotate", "translate","translateX", "scale", "translateY", "skew", "skewX", "skewY",
                "hue-rotate", "sepia", "blur", "infinite", "linear",
                "black", "white", "red", "transparent", "green", "blue", "yellow", "pink", "gray",
                "darkgray",
                "url",
            ]
        },
        "coloration" : ["Propriétés", "Valeurs", "Balises", "Classes", "Ids", "Accolades", "Unités", "Commentaires"]
    },

    ## Partie du langage PHP

    "PHP":{
        "exts" : ["php"],
        "keywords" : {
            "types": [
                "string", "int", "float"
            ],
            "functions": [
                "array", "__construct", "__destruct"
            ],
            "words": [
                "class", "function", "if", "elseif", "else", "while", "do", "for", "echo", "include", "require"
            ]
        },
        "coloration" : ["Chaines", "Nombres", "Mots clés 1", "Types", "Fonctions", "Commentaires"]
    }
}

"""--- Classement des mots clés par ordre alphabétique ----------"""

sorted(LANGUAGES["HTML"]["keywords"]["tags"])
sorted(LANGUAGES["HTML"]["keywords"]["attributes"])

sorted(LANGUAGES["CSS"]["keywords"]["properties"])

sorted(LANGUAGES["PHP"]["keywords"]["types"])
sorted(LANGUAGES["PHP"]["keywords"]["functions"])
sorted(LANGUAGES["PHP"]["keywords"]["words"])