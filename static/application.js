$(function() {
    // Ajax long polling connection
    var connection;
    
    // Canvas context
    var canvas = $("#canvas")[0];
    var context = canvas.getContext("2d");
    var offset = $('#canvas').offset();
    var drawing = false;
    var prevX, prevY;
    
    context.lineWidth = 12;
    context.strokeStyle = 'black';
    context.stroke();
    
    // Drawing functions
    var drawstart = function(e) {
        var x = e.pageX - offset.left;
        var y = e.pageY - offset.top;
        drawing = true;
        context.beginPath();
        context.moveTo(x, y);
    }
    
    var drawmove = function(e) {
        if (drawing) {
            var x = e.pageX - offset.left;
            var y = e.pageY - offset.top;
            context.lineTo(x, y);
            context.stroke();
        }
    }
    
    var drawend = function(e) { drawing = false; }
    
    $("#canvas").mousedown(drawstart);
    $("#canvas").on('touchstart', function(e) {
        drawstart(e.originalEvent.touches[0]);
        e.stopPropagation();
        e.preventDefault();
    });
    
    $('#canvas').mousemove(drawmove);
    $('#canvas').on('touchmove', function(e) {
        drawmove(e.originalEvent.touches[0]);
        e.stopPropagation();
        e.preventDefault();
    });
    
    $("#canvas").mouseup(drawend);
    $('#canvas').mouseleave(drawend);
    $('#canvas').on('touchend', function(e) {
        drawend(e.originalEvent.touches[0]);
        e.stopPropagation();
        e.preventDefault();
    });
    
    // Recognize digit
    $("#btn-recognize").click(function(e) {
        $("#result").text('...');
        
        $.ajax({ url: "/recognize", type: 'POST', data: { image: canvas.toDataURL('image/png') },
            complete: function() {
                connection.abort();
        }, dataType: "json"});
        return false;
    });
    
    // Clear canvas
    $("#btn-clear").click(function(e) {
        context.clearRect(0, 0, canvas.width, canvas.height);
        return false;
    });
    
    // Get the result
    (function longpoll() {
        connection = $.ajax({ url: "/result", success: function(data) {
            $("#result").text(data.result);
        }, dataType: "json", timeout: 30000, complete: longpoll });
    })();
});
