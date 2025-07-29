OUTLINE =  """
if (window.outlineElement) {
    window.outlineElement.style.cssText = window.outlineElement.style.cssText.replace(/outline: [A-z 0-9]+!important;/, '');
}
window.outlineElement = self;
window.outlineElement.style.cssText = window.outlineElement.style.cssText + '; outline: 2px fuchsia solid !important;'
window.outlineElement.scrollIntoView({
    block: "center"
});
"""

OUTLINE_LIST = """
if (window.locatorElements) {
    window.locatorElements.forEach(function (locatorElement) {
        locatorElement.style.cssText = locatorElement.style.cssText.replace(/outline: [A-z 0-9]+!important;/, '');
    });
}
window.locatorElements = arguments[0];
window.locatorElements.forEach(function (locatorElement) {
    locatorElement.scrollIntoView({
        block: "center"
    });
    locatorElement.style.cssText = locatorElement.style.cssText + '; outline: 2px fuchsia solid !important;'
});
"""

GET_TEXT = """
switch (self.nodeName.toLowerCase()) {
    case 'input':
    case 'textarea':
        return self.value;
    default:
        return self.innerText;
}
"""

CLICK = "self.click();"
SCROLL_BY = "self.scrollBy(arguments[0],arguments[1])"
WINDOW_SCROLL_BY = "window.scrollBy(arguments[0],arguments[1])"
WINDOW_SCROLL_TO = "window.scrollTo(arguments[0],arguments[1])"
DOCUMENT_READY_STATE = "return document.readyState;"
CLEAR = "self.value = '';"