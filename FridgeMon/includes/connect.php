<?php
$servername = "plesk.remote.ac";
$username = "ws330240_Projects";
$password = "M0nday08#";
$database="ws330240_AandR";

// Create connection
$conn = new mysqli($servername, $username, $password,$database);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
echo "";
?>