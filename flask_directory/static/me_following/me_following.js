const wrapper = document.querySelector(".sub_search"),
      textInput = document.querySelector(".sub_search > input[type='text']");

textInput.addEventListener("keyup", event => {
  wrapper.setAttribute("data-text", event.target.value);
});

function unUser(n) {
  var change = document.getElementsByClassName("unsubscribe_user");
  change[n].className = "unsubscribe_user";

  if (change[n].innerHTML != "Подписаться")
  {
    change[n].innerHTML = "Подписаться";
    change[n].style.backgroundColor = "#288700"
    change[n].style.color = "rgb(255,255,255)"
    $('.unsubscribe_user').addClass('spec_del_green');
  } else {
    change[n].innerHTML = "Отписаться";
    change[n].style.backgroundColor = "#950000"
    change[n].style.color = "#ffffff" //Текст при нажатии
    $('.unsubscribe_user').addClass('spec_del_red');
  }
}
