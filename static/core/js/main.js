function showPopup(html)
{
    popup_content.innerHTML = "";
    if (typeof html == "string") {
        popup_content.innerHTML = html;
    } else {
        popup_content.appendChild(html);
    }
    popup.setAttribute('style','display: block');
    document.body.style.overflow = "hidden"
}
function hidePopup()
{
    popup.setAttribute('style','display: none');
    document.body.style.overflow = "auto"
}

function _showLoadingAnimation(elem)
{
    if (typeof loading_element !== 'undefined') {
        loading_element.textContent += '.';
        setTimeout(_showLoadingAnimation, 1000);
    }
}

function showLoadingAnimation(elem)
{
    elem.innerHTML = '<h1 id="loading_element">Загрузка...</h1>';

    _showLoadingAnimation(elem);
}

function showError(elem, text)
{
    elem.innerHTML = '<h1 id="error_element">' + text + '</div>';
}