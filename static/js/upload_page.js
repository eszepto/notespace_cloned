
var i = 0;
var k = 0;
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
            
            

            i+=1;

            $('#form_img').append(`<img id="img_id" src=""  class="${i}" style="max-width:300px;max-height: 300px;" > `)
            $('#form_img').append(`<br  class="${i}"/> `)
        
        }

        reader.readAsDataURL(input.files[j]);
    }
    k += 1
    $('#file_input').attr('id',"")
    $('#file_field').append(`<input id="file_input" type="file" style="display: none;" onchange="upload_img_multiple(this)" name="${k}" multiple>`)
}

function delete_img(button) {
    $(`.${button.className}`).remove();
}