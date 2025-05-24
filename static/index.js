$(document).ready(function () {
  $("#promptInput").on('keypress', function (e) {
    if (e.which === 13) {
      const promptInput = $("#promptInput").val().trim();
      if (!promptInput) return;

      $("#response").append(`<p class="user-input chat-message">${promptInput}</p>`);
      $("#promptInput").val('');
      $("#promptInput").prop('disabled', true);

      addLoadingSpinner();

      // ====== DEBUG =======
      // setTimeout(() => {
      //   removeLoadingSpinner(); // Hide the spinner
      //   // Simulate success or error
      //   const apiResponseText = "<p>This is an AI response to: '" + promptInput + "'.</p>";
      //   $("#response").append(apiResponseText);
      //   $("#promptInput").prop('disabled', false); // Re-enable input
      //   $('#promptInput').focus();
      // }, 1000); // Simulate a 2-second API call delay
      // ====== DEBUG =======

      $.ajax({
        url: '/ask',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ prompt: promptInput }),
        success: function (data) {
          // const responseHtml = `<div class="alert alert-success mt-3" role="alert">${data.response}</div>`;
          removeLoadingSpinner();
          addApiResponse(data.response);
          $("#promptInput").prop('disabled', false); // Re-enable input
          $('#promptInput').focus();
        },
        error: function (xhr, status, error) {
          // const errorHtml = `<div class="alert alert-danger mt-3" role="alert">Something went wrong: ${error}</div>`;
          removeLoadingSpinner();
          addApiResponse(error);
          $("#promptInput").prop('disabled', false); // Re-enable input
          $('#promptInput').focus();
        }
      });
    }
  });
});

function scrollDown(){
  $("#response").scrollTop($("#response")[0].scrollHeight);
}

function addLoadingSpinner(){
  let spinner = '<div class="chat-message api-response loading-spinner-message" id="loadingSpinner"><div class="spinner-grow spinner-grow-sm" role="status"><span class="visually-hidden">Loading...</span></div></div>';
  $("#response").append(spinner);
  scrollDown();
}

function removeLoadingSpinner(){
  $("#loadingSpinner").remove();
}

function addApiResponse(ReplyText){
  const responseContainer = $("#response");
  const apiMessageDiv = $('<div class="chat-message api-response"></div>');
  responseContainer.append(apiMessageDiv);
  scrollDown();
  let charIndex = 0;

  function typeCharacter(){
    if(charIndex < ReplyText.length){
      apiMessageDiv.text(apiMessageDiv.text() + ReplyText.charAt(charIndex));
      charIndex++;

      let typeSpeed = Math.floor(Math.random() * 20) + 10;

      setTimeout(typeCharacter, typeSpeed);
      if(charIndex % 5 === 0){
        scrollDown();
      }
    }else{
      scrollDown();
    }
  }

  typeCharacter();
}