<?php
$dbConn->GetAll('SELECT * FROM campaigns WHERE FIND_IN_SET (id, ' . $dbConn->Param(”) . ')', array(join(',', $ids)));
