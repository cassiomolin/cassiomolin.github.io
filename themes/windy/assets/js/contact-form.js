import * as params from "@params";

function loaded() {
  const form = document.getElementById(params.formId);
  form.addEventListener("submit", handleFormSubmit);
}

document.addEventListener("DOMContentLoaded", loaded);

function isHuman(honeypot) {
  return !!honeypot;
}

function getFormData(form) {
  const fields = Array.from(form.elements)
    .map(element => element.name || (element.length > 0 && element.item(0).name))
    .filter((item, pos, self) => self.indexOf(item) === pos && item);

  const formData = {};
  fields.forEach(name => {
    const element = form.elements[name];
    formData[name] = element.value;

    if (element.length) {
      const data = Array.from(element)
        .filter(item => item.checked || item.selected)
        .map(item => item.value);
      formData[name] = data.join(", ");
    }
  });

  formData.formDataNameOrder = JSON.stringify(fields);
  formData.formGoogleSheetName = form.dataset.sheet || "Messages";
  formData.formGoogleSendEmail = form.dataset.email || "";

  return formData;
}

async function handleFormSubmit(event) {

  console.log("Handling for submission");
  event.preventDefault();

  const form = event.target;
  const data = getFormData(form);

  if (isHuman(data.website)) {
    messageSent(form);
    return false;
  }

  disableAllButtons(form);
  const url = params.contactFormUrl;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams(data)
    });

    if (response.ok) {
      messageSent(form);
    }
  } catch (error) {
    console.error("Error: ", error);
  }
}

function disableAllButtons(form) {
  const buttons = form.querySelectorAll("button");
  buttons.forEach(button => {
    button.disabled = true;
    button.textContent = "Sending...";
    button.classList.add("cursor-wait");
  });
}

function messageSent(form) {
  form.style.display = "none";
  const messageSent =  document.getElementById(params.messageSentId);
  messageSent.style.display = "block";
}
