
var i = 0;
function upload_img_multiple(input){
    let len = input.files.length
    for(let j=0; j<len; j++)
    {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#img_id').before(`<button onclick="delete_img(this)" class="${i}">X</button>
                                    <br class="${i}"/>`)
            $('#img_id').attr('src', e.target.result);
            $('#img_id').attr('id', "")
            $('#file_input').hide()
            $('#file_input').attr('id',"")
            i+=1;

            $('#form_img').append(`<img id="img_id" src=""  class="${i}" style="max-width:300px;max-height: 300px;" > `)
            $('#form_img').append(`<br  class="${i}"/> `)
            $('#form_img').append(`<input id="file_input" type="file" class="${i}"  onchange="upload_img_multiple(this)" multiple> `)
        
        }

        reader.readAsDataURL(input.files[j]);
    }
}

function delete_img(button) {
    $(`.${button.className}`).remove();
}