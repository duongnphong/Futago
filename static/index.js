$(document).ready(function () {
  $("#promptInput").on('keypress', function (e) {
    if (e.which === 13) {
      const promptInput = $("#promptInput").val().trim();
      if (!promptInput) return;

      $("#response").append(`<p class="user-input chat-message">${promptInput}</p>`);
      $("#promptInput").val('');

      addLoadingSpinner();

      $.ajax({
        url: '/ask',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ prompt: promptInput }),
        success: function (data) {
          // const responseHtml = `<div class="alert alert-success mt-3" role="alert">${data.response}</div>`;
          removeLoadingSpinner();
          const responseHtml = `<p class="api-response chat-message">${data.response}</p>`;
          $("#response").append(responseHtml);
          scrollDown();
        },
        error: function (xhr, status, error) {
          // const errorHtml = `<div class="alert alert-danger mt-3" role="alert">Something went wrong: ${error}</div>`;
          removeLoadingSpinner();
          const errorHtml = `<p class="api-response chat-message">Something went wrong: ${error}</p>`;
          $("#response").append(errorHtml);
          scrollDown();
        }
      });
    }
  });
});

function scrollDown(){
  $("#response").scrollTop($("#response")[0].scrollHeight);
}

function addLoadingSpinner(){
  let spinner = '<div class="spinner-grow" role="status" id="loadingSpinner"><span class="visually-hidden">Loading...</span></div>';
  $("#response").append(spinner);
  scrollDown();
}

function removeLoadingSpinner(){
  $("#loadingSpinner").remove();
}