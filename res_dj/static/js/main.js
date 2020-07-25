function post_res() {
  $.post("/autores/res",{
    number: $("#number").text(),
    password: $("#pwd").text(),
    area: $("#area").text(),
    pos: $("#pos").text(),
    start: $("#start").text(),
    end: $("#end").text(),
    email:$("#email").text(),
    qr:$("qr").text(),
  },function (data,staus) {
    alert("数据: \n" + data + "\n状态: " + status);
  })
}
