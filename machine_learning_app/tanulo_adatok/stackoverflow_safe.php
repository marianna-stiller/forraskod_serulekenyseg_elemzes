<?php
/* check connection */
if (mysqli_connect_errno()) {
    file_put_contents('MySQLiErrors.txt',date('[Y-m-d H:i:s]'). mysqli_connect_error()."\r\n", FILE_APPEND); 
    exit();
}else{
     $statement = $db->prepare("SELECT * FROM productcomment WHERE ProductId = ? LIMIT 1");
     $statement->bind_param("s", $input);


}
