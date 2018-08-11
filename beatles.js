//Random Movement - http://www.btinternet.com/~kurt.grigg/javascript

function beatles(img){
    
    var rm_img = new Image();
    rm_img.src = img;

    var imgh = 163;
    var imgw = 156;
    var timer = 40; //setTimeout speed.
    var min = 1;    //slowest speed.
    var max = 5;    //fastest speed.

    var idx = 1;
    idx = parseInt(document.images.length);
    if (document.getElementById("pic"+idx)) idx++;
    
    var stuff = "<div id='pic"+idx+"' style='position:absolute;"
	+"top:2px;left:2px;height:"+imgh+"px;width:"+imgw+"px;"
	+"overflow:hidden'><img src='"+rm_img.src+"' alt=''/><\/div>";
    document.write(stuff);

    var h,w,r,temp;
    var d = document;
    var y = 2;
    var x = 2;
    var dir = 45;   //direction.
    var acc = 1;    //acceleration.
    var newacc = new Array(1,0,1);
    var vel = 1;    //initial speed.
    var sev = 0;
    var newsev = new Array(1,-1,2,-2,0,0,1,-1,2,-2);

    //counters.
    var c1 = 0;    //time between changes.
    var c2 = 0;    //new time between changes.
    
    var pix = "px";
    var domWw = (typeof window.innerWidth == "number");
    var domSy = (typeof window.pageYOffset == "number");
    
    if (domWw) r = window;
    else{
	if (d.documentElement &&
	    typeof d.documentElement.clientWidth == "number" &&
	    d.documentElement.clientWidth != 0)
	    r = d.documentElement;
	else{
	    if (d.body &&
		typeof d.body.clientWidth == "number")
		r = d.body;
	}
    }
    


    function winsize(){
	var oh,sy,ow,sx,rh,rw;
	if (domWw){
	    if (d.documentElement && d.defaultView &&
		typeof d.defaultView.scrollMaxY == "number"){
		oh = d.documentElement.offsetHeight;
		sy = d.defaultView.scrollMaxY;
		ow = d.documentElement.offsetWidth;
		sx = d.defaultView.scrollMaxX;
		rh = oh-sy;
		rw = ow-sx;
	    }
	    else{
		rh = r.innerHeight;
		rw = r.innerWidth;
	    }
	    h = rh - imgh;
	    w = rw - imgw;
	}
	else{
	    h = r.clientHeight - imgh;
	    w = r.clientWidth - imgw;
	}
    }


    function scrl(yx){
	var y,x;
	if (domSy){
	    y = r.pageYOffset;
	    x = r.pageXOffset;
	}
	else{
	    y = r.scrollTop;
	    x = r.scrollLeft;
	}
	return (yx == 0)?y:x;
    }


    function newpath(){
	sev = newsev[Math.floor(Math.random()*newsev.length)];
	acc = newacc[Math.floor(Math.random()*newacc.length)];
	c2 = Math.floor(20+Math.random()*50);
    }


    function moveit(){
	var vb,hb,dy,dx,curr;
	if (acc == 1) vel +=0.05;
	if (acc == 0) vel -=0.05;
	if (vel >= max) vel = max;
	if (vel <= min) vel = min;
	c1++;
	if (c1 >= c2){
	    newpath();
	    c1=0;
	}
	curr = dir+=sev;
	dy = vel * Math.sin(curr*Math.PI/180);
	dx = vel * Math.cos(curr*Math.PI/180);
	y+=dy;
	x+=dx;
	//horizontal-vertical bounce.
	vb = 180-dir;
	hb = 0-dir;
	//Corner rebounds?
	if ((y < 1) && (x < 1)){y = 1; x = 1; dir = 45;}
	if ((y < 1) && (x > w)){y = 1; x = w; dir = 135;}
	if ((y > h) && (x < 1)){y = h; x = 1; dir = 315;}
	if ((y > h) && (x > w)){y = h; x = w; dir = 225;}
	//edge rebounds.
	if (y < 1) {y = 1; dir = hb;}
	if (y > h) {y = h; dir = hb;}
	if (x < 1) {x = 1; dir = vb;}
	if (x > w) {x = w; dir = vb;}

	//Assign it all to image.
	temp.style.top = y + scrl(0) + pix;
	temp.style.left = x + scrl(1) + pix;
	setTimeout(moveit,timer);
    }

    function init(){
	temp = document.getElementById("pic"+idx);
	winsize();
	moveit();
    }


    if (window.addEventListener){
	window.addEventListener("resize",winsize,false);
	window.addEventListener("load",init,false);
    }
    else if (window.attachEvent){
	window.attachEvent("onresize",winsize);
	window.attachEvent("onload",init);
    }

};

function demo(){
    beatles("./demo.gif");
}
beatles("./demo.gif");
