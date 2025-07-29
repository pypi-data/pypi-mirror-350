import $ from "jquery";
import "semantic-ui-css";
import { MultipleOptionsSearchBar } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/invenio_app_rdm/i18next";
import ReactDOM from "react-dom";
import React from "react";

// called on document ready
$(function () {
    importZammadScript();
    syncLogoHover();
});

function importZammadScript() {
    let scriptNode = document.createElement("hidden"); //needed for zammad script
    scriptNode.id = "zammad_form_script";
    scriptNode.src = "https://ub-support.tugraz.at/assets/form/form.js";
    document.head.appendChild(scriptNode);

    $.getScript("https://ub-support.tugraz.at/assets/form/form.js", () => {
        $("#feedback-form").ZammadForm({
            messageTitle: "Contact us",
            showTitle: true,
            messageSubmit: "Submit",
            messageThankYou:
                "Thank you for your message, (#%s). We will get back to you as quickly as possible!",
            modal: true,
        });
    });
}

// used for sticky test instance notification
$(".ui.sticky.test-instance").sticky({
    context: "body",
});

export function toggleVisibility(id) {
    var element = document.getElementById(id);
    var isHided = element.style.display === "none";

    element.style.display = isHided ? "block" : "none";
}

window.toggleVisibility = toggleVisibility;

const headerSearchbar = document.getElementById("header-search-bar");
const searchBarOptions = JSON.parse(headerSearchbar.dataset.options);

// Synchronises the hover states of the subcomponents of the logo
export function syncLogoHover() {
    const logoGrad = document.getElementById("int-header-logo-grad");
    const logoText = document.getElementById("int-header-logo-text");

    const originalFillGrad = logoGrad.getAttribute("fill");
    const originalColorGrad = logoGrad.getAttribute("color");
    const originalFillText = logoText.getAttribute("fill");
    const originalColorText = logoText.getAttribute("color");

    logoGrad.addEventListener("mouseover", () => {
        logoText.setAttribute("fill", "@primaryLinkHoverBackground");
        logoText.setAttribute("color", "@primaryLinkHoverBackground");
    });
    logoGrad.addEventListener("mouseout", () => {
        logoText.setAttribute("fill", originalFillText);
        logoText.setAttribute("color", originalColorText);
    });

    logoText.addEventListener("mouseover", () => {
        logoGrad.setAttribute("fill", "@primaryLinkHoverBackground");
        logoGrad.setAttribute("color", "@primaryLinkHoverBackground");
    });
    logoText.addEventListener("mouseout", () => {
        logoGrad.setAttribute("fill", originalFillGrad);
        logoGrad.setAttribute("color", originalColorGrad);
    });
}

window.syncLogoHover = syncLogoHover;

ReactDOM.render(
    <MultipleOptionsSearchBar
        options={searchBarOptions}
        placeholder={i18next.t("Search records...")}
    />,
    headerSearchbar,
);
