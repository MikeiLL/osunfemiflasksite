import {
    lindt,
    choc,
    replace_content,
    on,
    DOM,
} from "https://rosuav.github.io/choc/factory.js";
const {FORM, INPUT, LABEL} = lindt; //autoimport
import {simpleconfirm} from "./utils.js";


on("click", ".tithe", async (e) => {
  let resp = await fetch("/payment/create-checkout-session",
    {
      method: "POST",
      headers: {"content-type": "application/json"},
      body: JSON.stringify({
        "price_id": e.match.id
      }),
    }
  );
  let result = await resp.json();
  window.location = result.url;
});
on("click", "button#signup", (e) => {
  replace_content("dialog#main", [
    FORM({id: "signup"}, [
      LABEL([INPUT({name: "fullname", "aria-required": true, "required": true}), "Full Name"]),
      LABEL([INPUT({name: "orishaname"}), "Ifa/Orisha Name"]),
      LABEL([INPUT({name: "email", type: "email", "aria-required": true, "required": true}), "Email"]),
      LABEL([INPUT({name: "password", type: "password", "aria-required": true, "required": true, minlength: 12}), "Password (at least 12 characters)"]),
      INPUT({type: "submit"}, "Submit"),
    ]),
  ]);
  DOM("dialog#main").showModal();
});
on("submit", "form#signup", async (e) => {
  e.preventDefault();
  console.log(e.match);
  let formData = new FormData(e.match);
  console.log(JSON.stringify(Object.fromEntries(formData)));
  let response = await fetch("/signup", {
    method: "POST",
    body: new FormData(e.match),
  });
  let result = await response.json();
  console.log(result);
})
