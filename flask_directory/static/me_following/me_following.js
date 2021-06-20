const wrapper = document.querySelector(".sub_search"),
      textInput = document.querySelector(".sub_search > input[type='text']");

textInput.addEventListener("keyup", event => {
  wrapper.setAttribute("data-text", event.target.value);
});

function unUser() {
  var change = document.getElementById("unsubscribe_user");
  if (change.innerHTML == "Отписаться")
  {
    change.innerHTML = "Подписаться";
  }
  else {
    change.innerHTML = "Отписаться";
  }
}