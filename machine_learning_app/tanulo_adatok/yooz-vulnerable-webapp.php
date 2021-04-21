	<?php
	if (isset($_GET['id'])) {
		$id = $_GET["id"];
		include("config/config.php");
		$conn = new mysqli($_sv, $_user, $_pass, $_dbnamegi);
		if ($conn->connect_error) {
			die("Connection failed: " . $conn->connect_error);
		}
		$sql = "SELECT id, user, email FROM login WHERE id='$id'";
		echo 'The Query is : ' . $sql;
		$res = $conn->query($sql);

		if ($res && $res->num_rows > 0) {
			while ($row = $res->fetch_assoc()) {
				echo "<div class='alert alert-info text-center'>You Can Contact Me By This Email :<br/>" . $row['email'] . "</div>";
			}
		} else {
			echo "0 results";
		}
		$conn->close();
	} else {
		echo "<div class='alert alert-info'>Use 'id' parameter as input value or <a href='?vuln=sql_injection&id=1'>click here </a></div>";
	}
	?>