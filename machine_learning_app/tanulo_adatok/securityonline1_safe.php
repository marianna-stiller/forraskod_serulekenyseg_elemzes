<?php
$dbConn->GetRow("SELECT * FROM users WHERE id = ?", array('$user_id'));
