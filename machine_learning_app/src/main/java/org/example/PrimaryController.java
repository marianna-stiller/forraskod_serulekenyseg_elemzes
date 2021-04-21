package org.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ArrayList;
import java.util.ResourceBundle;

import javafx.beans.binding.Binding;
import javafx.beans.binding.Bindings;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.chart.PieChart;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.stage.Stage;

public class PrimaryController implements Initializable {
    @FXML
    public Label result;
    @FXML
    public PieChart piechart;
    @FXML
    public Button button2;
    @FXML
    public Button button3;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        ArrayList<String> list = null;
        try {
            Runtime runtime = Runtime.getRuntime();
            runtime.exec("node parser.js");
            runtime.exec("py nodes.py");
            runtime.exec("py vectorizer.py");
            Process process = runtime.exec("py tanulo.py");
            InputStream is = process.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);
            String line;
            list = new ArrayList<String>();
            while ((line = br.readLine()) != null) {
                list.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        assert list != null;
        double vulnerable = Double.parseDouble(list.get(0));
        double notvulnerable = Double.parseDouble(list.get(1));
        ObservableList<PieChart.Data> pieChartData = FXCollections.observableArrayList(
                        new PieChart.Data("Sérülékeny",vulnerable*100),
                        new PieChart.Data("Nem sérülékeny",notvulnerable*100));
        piechart.setData(pieChartData);
            pieChartData.forEach(data -> {
                data.nameProperty().bind(Bindings.concat(data.getName()," [",data.pieValueProperty(),"%]"));
                if(vulnerable > 0.5) {
                    piechart.getStylesheets().add("css/style.css");
                } else {
                    piechart.getStylesheets().add("css/style2.css");
                }
            });
    }

    public void back(ActionEvent actionEvent) throws IOException {
        Stage stage = (Stage) button2.getScene().getWindow();
        stage.close();

        Parent root = FXMLLoader.load(getClass().getResource("first.fxml"));
        Scene scene = new Scene(root);
        stage.setScene(scene);
        stage.show();
    }

    public void close(ActionEvent actionEvent) {
        Stage stage = (Stage) button3.getScene().getWindow();
        stage.close();
    }
}
