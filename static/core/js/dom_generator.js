function createElement(tagName, text, attributes, events)
{
    var element = document.createElement(tagName);
    element.textContent = text;

    console.log(attributes);
    attributes.keys.forEach(function(k){
        element[k] = attributes.values[k];
    });


    return element
}
function generateDOM(elements, parent)
{
    elements.forEach(function(elem, i) {
        var createdElem; 
        var tagName = elem.tag || 'div';
        var content;

        if(elem.content instanceof Array || typeof elem.content == 'undefined')
            content = '';
        else
            content = elem.content;

        var attributes = {};
        attributes.keys = Object.keys(elem).filter(function(k){
            return (k !== 'tag') && (k !== 'content')
        });          
        attributes.values = elem;



        createdElem = createElement(tagName, content, attributes);

        if(elem.content instanceof Array)
         generateDOM(elem.content, createdElem);

     parent.appendChild(createdElem);

 });
    return parent;
}