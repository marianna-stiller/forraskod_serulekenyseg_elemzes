<?php	
$username = mysqli_real_escape_string($conn,$_POST["username"]);
$password = mysqli_real_escape_string($conn,$_POST["password"]);
mysqli_close($conn);
?>