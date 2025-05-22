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
          const responseHtml = `<div class="alert alert-success mt-3" role="alert">${data.response}</div>`;
          $("#main").append(responseHtml);
        },
        error: function (xhr, status, error) {
          const errorHtml = `<div class="alert alert-danger mt-3" role="alert">Something went wrong: ${error}</div>`;
          $("#main").append(errorHtml);
        }
      });

      $("#promptInput").val('');
    }
  });
});
