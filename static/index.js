$(document).ready(function () {
  $("#promptInput").on('keypress', function (e) {
    if (e.which === 13) {
      const promptInput = $("#promptInput").val().trim();
      if (!promptInput) return;

      $.ajax({
        url: '/ask',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ prompt: promptInput }),
        success: function (data) {
          // const responseHtml = `<div class="alert alert-success mt-3" role="alert">${data.response}</div>`;
          const responseHtml = `<p>${data.response}</p>`;
          $("#response").append(responseHtml);
        },
        error: function (xhr, status, error) {
          // const errorHtml = `<div class="alert alert-danger mt-3" role="alert">Something went wrong: ${error}</div>`;
          const errorHtml = `<p>Something went wrong: ${error}</p>`;
          $("#response").append(errorHtml);
        }
      });

      $("#promptInput").val('');
    }
  });
});
