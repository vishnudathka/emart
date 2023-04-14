//bootstrapfy form
document.addEventListener("DOMContentLoaded", function () {
  // Get all Django forms on the page
  const djangoForms = document.querySelectorAll("form");
  djangoForms.forEach((form) => {
    console.log(form);
    Array.from(form.elements).forEach((ele) => {
      let tagName = ele.tagName.toLowerCase();
      let type = ele.type ? ele.type.toLowerCase() : "";

      if (
        tagName === "input" ||
        tagName === "textarea" ||
        tagName === "select"
      ) {
        ele.classList.add("form-control");
        if (tagName === "select") {
          ele.parentElement.classList.add("form-group");
        }
        const label = ele.previousElementSibling;
        if (label && label.tagName.toLowerCase() === "label") {
          label.classList.add("form-label");
        }
        if (type === "checkbox" || type === "radio") {
          ele.parentElement.classList.add("form-check");
          ele.classList.add("form-check-input");
          label.classList.add("form-check-label");
        }
        const helpText = ele.nextElementSibling;
        if (helpText && helpText.classList.contains("helptext")) {
          helpText.classList.add("form-text");
        }
        const errorList = ele.parentElement.nextElementSibling;
        if (errorList && errorList.tagName.toLowerCase() === "ul") {
          errorList.classList.add("form-text");
        }
      }
    });
  });
});
