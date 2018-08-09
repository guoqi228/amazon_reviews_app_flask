function checkEmpty() {
  var input = $("#productId").val();
  if (input != "") {
    $("#submit").attr("data-toggle","modal");
  }
}
