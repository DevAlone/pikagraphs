function showPopup(html)
{
    popup_content.innerHTML = html;
    popup.setAttribute('style','display: block');
    document.body.style.overflow = "hidden"
}
function hidePopup()
{
    popup.setAttribute('style','display: none');
    document.body.style.overflow = "auto"
}