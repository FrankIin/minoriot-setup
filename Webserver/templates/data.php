<?php

try {

    $db = new SQLite3('../sensor_data.db');

    $reponse = $db->query("SELECT timestamp, temperature FROM sensor_data");

    $rows = array();
    $rows['time'] = 'timestamp';
    $rows1 = array();
    $rows1['temperature'] = 'temperature';

    while ($valeur = $reponse->fetchArray())
    {
        $rows['data'][] = $valeur['time'];
        $rows1['data'][] = $valeur['temperature'];
    }

} catch(Exception $e) {
    echo "ERROR DATABASE";
    die();
}

$result = array();
array_push($result,$rows);
array_push($result,$rows1);

print json_encode($result, JSON_NUMERIC_CHECK);

 ?>