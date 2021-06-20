const wrapper = document.querySelector(".followers_search_block"),
      textInput = document.querySelector(".followers_search_block > input[type='text']");

textInput.addEventListener("keyup", event => {
  wrapper.setAttribute("data-text", event.target.value);
});


function delUser(n) {
  var change = document.getElementsByClassName("delete_follower");
  var color1 = '#ED4956';
  var color2 = '#4ACFFF';

  if (change[n].innerHTML == "Заблокировать")
  {
    change[n].innerHTML = "Разблокировать";
  }
  else
  {
    change[n].innerHTML = "Заблокировать";
  }
}
// Осталось реализовать изменение цвета при нажатии на кнопку и прикрутить к ней стили