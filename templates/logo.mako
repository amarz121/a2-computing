<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">

<html>

<head>

<title>Student Record System </title>

<style>
#wrapper {
		max-width: 800px;
		margin: 0 auto;
		border: 2px solid #777777;
		border-top: 0;
		background: #ffffff 100% repeat-x;
		padding: 20px 20px 50px;
		font-family: "calibri"
		}

body {
		height:100%
		padding: 0 30px; 
		/* FF3.6+ */
		background: -moz-linear-gradient(top, rgba(3,66,106,0.93) 0%, rgba(144,181,209,0.65) 100%); 
		/* Chrome,Safari4+ */
		background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,rgba(3,66,106,0.93)), color-stop(100%,rgba(144,181,209,0.65)));
		/* Chrome10+,Safari5.1+ */		
		background: -webkit-linear-gradient(top, rgba(3,66,106,0.93) 0%,rgba(144,181,209,0.65) 100%); 
		 /* Opera 11.10+ */
		background: -o-linear-gradient(top, rgba(3,66,106,0.93) 0%,rgba(144,181,209,0.65) 100%);
		/* IE10+ */
		background: -ms-linear-gradient(top, rgba(3,66,106,0.93) 0%,rgba(144,181,209,0.65) 100%); 
		 /* W3C */
		background: linear-gradient(to bottom, rgba(3,66,106,0.93) 0%,rgba(144,181,209,0.65) 100%);
		/* IE6-9 */
		filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#ed03426a', endColorstr='#a690b5d1',GradientType=0 ); 
		}		
		
</style>

</head>

 <body>
		<div id="wrapper">
		
		   <a href="${ request.route_url('home') }"> 
	          <img src="http://ukwallball.co.uk/wp-content/uploads/2013/01/UCLA_logo.png" alt="UCLA Logo" height="200" width="190">
		   </a>
		   
		   ${ next.body() }
		   
		</div>
</body>

</html>
