import {
    lindt,
    choc,
    replace_content,
    on,
    DOM,
} from "https://rosuav.github.io/choc/factory.js";
const {A, BUTTON, FIELDSET, FORM, H2, H4, INPUT, LABEL, LEGEND, P} = lindt; //autoimport
import {simpleconfirm} from "./utils.js";

async function make_transaction(e) {
  let resp = true || await fetch("/payment/create-checkout-session",
    {
      method: "POST",
      headers: {"content-type": "application/json"},
      body: JSON.stringify({
        "price_id": e.match.id,
        "recurring": e.match.dataset.recurring+'',
      }),
    }
  );
  let result = await resp.json();
  if (result.url) {
    window.location = result.url;
  } else {
    console.log("replacing content");
    replace_content("dialog#main", [H2("Something went wrong."), P([result.error || '', result.message]), H4("Call Iya or better yet, email Pinpin at help@oghtolal.org.")])
  }
}

on("click", ".transaction", (e) => {
  if (e.match.dataset.loggedin) {
    make_transaction(e)
  } else {
    login(e);
  };
});

function login(e) {
  replace_content("dialog#main", [
    FORM({id: "login"}, [
      FIELDSET([
        LEGEND("Login"),
        LABEL([INPUT({name: "email", type: "email", "aria-required": true, "required": true}), "Email"]),
        LABEL([INPUT({name: "password", type: "password", "aria-required": true, "required": true, minlength: 12}), "Password"]),
        INPUT({type: "submit"}, "Submit"),
      ]),
    ]),
    BUTTON({id: "register", href: "forgotpassword"}, "Register"),
    A({href: "forgotpassword"}, "Forgot password"),
  ]);
  DOM("dialog#main").showModal();
}

on("submit", "form#login", async (e) => {
  e.preventDefault();
  let response = await fetch("/login", {
    method: "POST",
    body: new FormData(e.match),
  });
  let result = await response.json();
  if (result.error) {
    replace_content("dialog#main", [H2(result.error || "Something went wrong."), P(result.message), H4("Call Iya or better yet, email Pinpin at help@oghtolal.com.")])
  }
})
function signup(e) {
  replace_content("dialog#main", [
    FORM({id: "signup"}, [
      FIELDSET([
        LEGEND("Register"),
        LABEL([INPUT({name: "fullname", "aria-required": true, "required": true}), "Full Name"]),
        LABEL([INPUT({name: "orishaname"}), "Ifa/Orisha Name"]),
        LABEL([INPUT({name: "email", type: "email", "aria-required": true, "required": true}), "Email"]),
        LABEL([INPUT({name: "password", type: "password", "aria-required": true, "required": true, minlength: 12}), "Password (at least 12 characters)"]),
        INPUT({type: "submit"}, "Submit"),
      ])
    ]),
  ]);
  if (DOM("dialog#main:modal" === null)) DOM("dialog#main").showModal();
}
on("click", "button#signup", signup);
on("click", "button#register", signup);
on("submit", "form#signup", async (e) => {
  e.preventDefault();
  let response = await fetch("/signup", {
    method: "POST",
    body: new FormData(e.match),
  });
  let result = await response.json();
  if (result.error) {
    replace_content("dialog#main", [H2(result.error || "Something went wrong."), P(result.message), H4("Call Iya or better yet, email Pinpin at help@oghtolal.com.")])
  }
})
