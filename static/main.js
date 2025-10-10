import {
    lindt,
    choc,
    replace_content,
    on,
    DOM,
} from "https://rosuav.github.io/choc/factory.js";
const {BUTTON, DIV, FIELDSET, H2, H4, HEADER, INPUT, LEGEND, OPTION, P, SECTION, SELECT, TEXTAREA} = lindt; //autoimport
import {simpleconfirm} from "./utils.js";


on("click", ".title", async (e) => {
  let resp = await fetch("/payment/create-checkout-session",
    {
      method: "POST",
      headers: {"content-type": "application/json"},
      body: JSON.stringify({
        "price_id": e.match.id
      }),
    }
  );
  result = await JSON.parse(resp);
  console.log(result);
  //DOM("dialog#main").showModal();
});
