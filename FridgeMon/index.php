<?php
include 'includes/connect.php';
	?>
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="style/style.css">
<script
src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js">
</script>
</head>
<body>


<!-- Most recent temp -->
<!-- ------------------------------------------------------------------------------------------ -->
<div class="flex-container">
<h4>Most recent tempature recording:</h4>
  <div class="flex-item-left">
	  <?php 
	  $recenttemp="SELECT `Fridgetemp`.`Tempature` FROM `Fridgetemp` WHERE`ID` =(SELECT MAX(`ID`)FROM `Fridgetemp`)";

	 
	  $result = mysqli_query($conn,$recenttemp);

	  echo "<table>"; // start a table tag in the HTML

	  while($row = mysqli_fetch_array($result)){   //Creates a loop to loop through results
		  echo "<tr><td>" . htmlspecialchars($row['Tempature']);
	  }

	  echo "</table>"; //Close the table in HTML

	  

?>
	 </div>
  <div class="flex-item-right">
	
	  <?php 
	  $recentdate="SELECT `Fridgetemp`.`Date and time` FROM `Fridgetemp` WHERE`ID` =(SELECT MAX(`ID`)FROM `Fridgetemp`)";

	 
	  $result = mysqli_query($conn,$recentdate);

	  echo "<table>"; // start a table tag in the HTML

	  while($row = mysqli_fetch_array($result)){   //Creates a loop to loop through results
		  echo "<tr><td>" . htmlspecialchars($row['Date and time']);
	  }

	  echo "</table>"; //Close the table in HTML

	  

?>
	</div>
</div>


<!-- Hottest tempature -->
<!-- -------------------------------------------------------------------------------- -->
<div class="flex-container">
<h4>Hottest fridge Tempature:</h4>
  <div class="flex-item-left">
	  <?php 
	  $hottemp="SELECT `Fridgetemp`.`Tempature` FROM `Fridgetemp` WHERE`Tempature` =(SELECT MAX(`Tempature`)FROM `Fridgetemp`)";

	 
	  $result = mysqli_query($conn,$hottemp);

	  echo "<table>"; // start a table tag in the HTML

	  while($row = mysqli_fetch_array($result)){   //Creates a loop to loop through results
		  echo "<tr><td>" . htmlspecialchars($row['Tempature']);
	  }

	  echo "</table>"; //Close the table in HTML

	  

?>
	 </div>
  <div class="flex-item-right">
	
	  <?php 
	  $hotdate="SELECT `Fridgetemp`.`Date and time` FROM `Fridgetemp` WHERE`Tempature` =(SELECT MAX(`Tempature`)FROM `Fridgetemp`)";

	 
	  $result = mysqli_query($conn,$hotdate);

	  echo "<table>"; // start a table tag in the HTML

	  while($row = mysqli_fetch_array($result)){   //Creates a loop to loop through results
		  echo "<tr><td>" . htmlspecialchars($row['Date and time']);
	  }

	  echo "</table>"; //Close the table in HTML

	  

?>
	</div>
</div>

<!-- Graph showing trend -->

<div class="flex-container"> 
	<div class="flex-item-right">
		<p>Graph showing trend :</p>
	</div>
	<div class="flex-item-left">
		<canvas id="myChart" style="width:100%;max-width:700px"></canvas>
		<script>
		const xValues = [
			
			<?php 
			$graphtemp="SELECT `Fridgetemp`.`Tempature` FROM `Fridgetemp` ORDER BY `ID` ASC ";

			
			$result = mysqli_query($conn,$graphtemp);

			echo "<table>"; // start a table tag in the HTML

			while($row = mysqli_fetch_array($result)){   //Creates a loop to loop through results
				echo "<tr><td>" . htmlspecialchars($row['Tempature']);
			}

			echo "</table>"; //Close the table in HTML
		?>

		];
		const yValues = [7,8,8,9,9,9,10,11,14,14,15];

		new Chart("myChart", {
		type: "line",
		data: {
			labels: xValues,
			datasets: [{
			fill: false,
			lineTension: 0,
			backgroundColor: "rgba(0,0,255,1.0)",
			borderColor: "rgba(0,0,255,0.1)",
			data: yValues
			}]
		},
		options: {
			legend: {display: false},
			scales: {
			yAxes: [{ticks: {min: 6, max:16}}],
			}
		}
		});
		</script>
	</div>
</div>


<div class="flex-item-right">
	
test area
  </div>

<!--  flex box referance : https://www.w3schools.com/css/css3_flexbox_responsive.asp-->
</body>
</html>


