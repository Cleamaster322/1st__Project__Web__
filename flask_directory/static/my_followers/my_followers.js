const wrapper = document.querySelector(".followers_search_block"),
      textInput = document.querySelector(".followers_search_block > input[type='text']");

textInput.addEventListener("keyup", event => {
  wrapper.setAttribute("data-text", event.target.value);
});


function delUser(n) {
  var change = document.getElementsByClassName("delete_follower");
  change[n].className = "delete_follower";

  if (change[n].innerHTML == "Заблокировать")
  {
    change[n].innerHTML = "Разблокировать";
    change[n].style.borderColor = "#4ACFFF"
    change[n].style.color = "#4ACFFF"
    $('.delete_follower').addClass('spec_del_blue');
  }
  else
  {
    change[n].innerHTML = "Заблокировать";
    change[n].style.borderColor = "#ED4956"
    change[n].style.color = "#ED4956"
    $('.delete_follower').addClass('spec_del_red');
  }
}
// Осталось реализовать изменение цвета при нажатии на кнопку и прикрутить к ней стили