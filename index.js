var promptInput;

$("#promptInput").on('keypress', function(e){
  if(e.which == 13){
    promptInput = $("#promptInput").val();
    console.log(promptInput);
    $("#promptInput").val('');
  }
});