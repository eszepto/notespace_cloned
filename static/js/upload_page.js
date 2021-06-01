
var i = 0;

function upload_img_multiple(input){
    
    let len = input.files.length
    for(let j=0; j<len; j++)
    {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('.img-container').append(`
                <div class="col-4 img-preview ${i+j}">
                    <button id="delete-btn" onclick="delete_img(this)" class="${i+j}">&#x2715</button>
                    <img src="" id="img${i+j}" class="img-fluid ui-state-default">
                </div>
                `)
            $(`#img${i+j}`).attr('src', e.target.result);
        
        }

        reader.readAsDataURL(input.files[j]);
    }
    i += len
}

function delete_img(button) {
    $(`.${button.className}`).remove();
}