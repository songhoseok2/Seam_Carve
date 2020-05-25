$(document).ready(
    function()
    {
        var SERVER_URL = "http://localhost:5000";
        var img_original_width;
        var img_original_height;
        var img_current_width;
        var img_current_height;
        var uploaded_img = $(".resizable_img");
        var src = $('img').attr('src').split('/');
        var uploaded_img_name = src[src.length - 1];
        console.log("uploaded_img_name: " + uploaded_img_name);

        uploaded_img.on('load',function(){
            img_original_width = uploaded_img.width();
            img_original_height = uploaded_img.height();
            console.log("img original_width: " + img_original_width + ", " + "height: " + img_original_height);

            $(".resizable_img").resizable(
            {
                maxWidth: img_original_width,
                maxHeight: img_original_height,
                minWidth: 10,
                minHeight: 10
            });
        });

        $(".mouse_lift_area").mouseup(
        function()
        {
            img_current_width = uploaded_img.width();
            img_current_height = uploaded_img.height();
            console.log("width=" + img_current_width + ", " + "height=" + img_current_height);
            $.ajax({
                type: "POST",
                url: SERVER_URL + "/process",
                data:
                { 
                    "img_name": uploaded_img_name,
                    "width_scale": img_current_width / img_original_width
                },
                success: function(msg){
                    console.log("rescaling success");
                    // and then in @app route ('/process'), get that img using uploaded_img_name, make a new image called
                    // <original img name>_carved, and make make the actual carving. then make a get request in this current function
                }
            });
            


        });
    }
);