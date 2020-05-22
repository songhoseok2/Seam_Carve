$(document).ready(
    function()
    {
//        var width = $(".resizable").clientWidth;
//        var height = $(".resizable").clientHeight;
//        alert("width: " + width + ", height: " + height);

        $(".resizable").resizable(
        {
          maxHeight: 250,
          maxWidth: 350,
          minHeight: 150,
          minWidth: 200
        });

    //<!--            this thing currently working when mouse is lifted on the image.-->
    //<!--            keep a variable "changing picture", then set the mouse up to the entire page-->

        $(".resizable").mouseup(
        function()
        {
            console.log('changed');
        });
    }
);