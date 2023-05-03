$(document).ready(function() {
    $('#upload-button').click(function() {
      // open file dialog box
      var input = document.createElement('input');
      input.type = 'file';
      input.accept = 'audio/*';

      // when file is selected, update button text
      input.onchange = function() {
      var file = input.files[0];
      $('#upload-button').text(file.name);
      };
      input.click();
    });
});

$(document).ready(function() {
  $('#submit-button').click(function() {
    console.log("hhhhhhhhhhhhhhhhhhhhhhhhh")
  })
})