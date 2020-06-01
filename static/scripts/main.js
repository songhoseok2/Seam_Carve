$(document).ready(
    function()
    {
        var SERVER_URL = "http://localhost:5000";
        var img_original_width;
        var img_original_height;
        var img_current_width;
        var img_current_height;
        var uploaded_img = $(".resizable_img");
        var splitted = $('img').attr('src').split('/');
        var uploaded_img_name = splitted[splitted.length - 1];

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
                minHeight: 10,

                resize: function(event, ui) {
                    console.log("this: ");
                    console.log($(this));
                    $(this).position({
                        of: $("#resizable_img_container_id"),
                        my: "center center",
                        at: "center center"
                    })
                }
            });

            $(".ui-wrapper").position({
                of: $("#resizable_img_container_id"),
                my: "center center",
                at: "center center"
            })
        });

        $(".mouse_lift_area").mouseup(
        function()
        {
            if(!(img_current_width == uploaded_img.width() &&
               img_current_height == uploaded_img.height()))
            {
                img_current_width = uploaded_img.width();
                img_current_height = uploaded_img.height();
                console.log("img_name: " + uploaded_img_name + "width=" + img_current_width + ", " + "height=" + img_current_height);
                $.ajax({
                    type: "POST",
                    url: SERVER_URL + "/process",
                    data:
                    {
                        "img_name": uploaded_img_name,
                        "width_scale": img_current_width / img_original_width,
                        "height_scale": img_current_height / img_original_height
                    },
                    success: function()
                    {

                    },
                    error: function ()
                    {

                    },
                    complete: function ()
                    {
                        var original_image_path = $(".resizable_img").attr("src");
                        console.log("original_image_path:" + original_image_path);
                        splitted = original_image_path.split('.');
                        var carved_image_path = splitted[0] + "_carved." + splitted[1];
                        var d = new Date();
                        $("#carved_img_id").attr("src", carved_image_path + "?" + d.getTime());
                    }
                });
            }
        });
    }
);