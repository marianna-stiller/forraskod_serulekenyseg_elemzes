package org.example;

import javafx.beans.binding.Bindings;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.chart.PieChart;
import javafx.scene.control.Button;
import javafx.scene.control.Hyperlink;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.scene.control.TextArea;
import javafx.stage.Stage;

import java.awt.*;
import java.io.*;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Date;
import java.util.ResourceBundle;

public class PrimaryController implements Initializable {
    @FXML
    public Label result;
    @FXML
    public PieChart piechart;
    @FXML
    public Button button2;
    @FXML
    public Button button3;
    @FXML
    public Label rtime;
    @FXML
    public Label describe1;
    @FXML
    public ProgressBar progress;
    @FXML
    public Label progress_no;
    @FXML
    public Hyperlink prevent_more;
    @FXML
    public Hyperlink sqli_more;
    @FXML
    public TextArea the_code;


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        ArrayList<String> list = null;
        Date before_date = new Date();
        String line;
        long before_timeMilli = before_date.getTime();
        try {
            Runtime runtime = Runtime.getRuntime();
            runtime.exec("node parser.js");
            runtime.exec("py nodes.py");
            runtime.exec("py vectorizer.py");
            Process process = runtime.exec("py tanulo.py");
            InputStream is = process.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);

            list = new ArrayList<>();
            while ((line = br.readLine()) != null) {
                list.add(line);
            }
            progress.setProgress(100);
            progress_no.setText(progress.getProgress() +"%");
        } catch (IOException e) {
            e.printStackTrace();
        }
        Date after_date = new Date();
        long after_timeMilli = after_date.getTime();
        long runtime_in_mili = after_timeMilli - before_timeMilli;
        int runtime_in_sec = (int)((runtime_in_mili / 1000) % 60);
        rtime.setText(runtime_in_sec +" mp");

        var fileName = "tanulo_adatok/toimport_vulnerabilities.php";
        try (BufferedReader br = new BufferedReader(
                new FileReader(fileName, StandardCharsets.UTF_8))) {
            var sb = new StringBuilder();
            String lines;
            while ((lines = br.readLine()) != null) {
                sb.append(lines);
                sb.append(System.lineSeparator());
            }
            the_code.setText(String.valueOf(sb));
        } catch (IOException e) {
            e.printStackTrace();
        }

        assert list != null;
        double vulnerable = Double.parseDouble(list.get(0))*100;
        double notvulnerable = Double.parseDouble(list.get(1))*100;
        ObservableList<PieChart.Data> pieChartData = FXCollections.observableArrayList(
                        new PieChart.Data("Sérülékeny", Math.round(vulnerable)),
                        new PieChart.Data("Nem sérülékeny",Math.round(notvulnerable)));
        piechart.setData(pieChartData);
        pieChartData.forEach(data -> {
            data.nameProperty().bind(Bindings.concat(data.getName()," [",data.pieValueProperty(),"%]"));
            if(vulnerable > 50) {
                piechart.getStylesheets().add("css/style.css");
            } else {
                piechart.getStylesheets().add("css/style2.css");
            }
        });
        describe1.setText("A program "+Math.round(vulnerable)+"%-os (pontosabban "+vulnerable+"%-os) valószínűségűre állapította meg a kód sérülékenységét SQL Injection-el szemben.");
    }

    public void back() throws IOException {
        Stage stage = (Stage) button2.getScene().getWindow();
        stage.close();

        Parent root = FXMLLoader.load(getClass().getResource("first.fxml"));
        Scene scene = new Scene(root);
        stage.setScene(scene);
        stage.show();
    }

    public void close() {
        Stage stage = (Stage) button3.getScene().getWindow();
        stage.close();
    }

    public void openWeb() {
        prevent_more.setOnAction(actionEvent -> {
            try {
                Desktop.getDesktop().browse(new URI("https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"));
            } catch (IOException | URISyntaxException e) {
                e.printStackTrace();
            }
        });
    }

    public void openWeb2() {
        sqli_more.setOnAction(actionEvent -> {
            try {
                Desktop.getDesktop().browse(new URI("https://owasp.org/www-community/attacks/SQL_Injection"));
            } catch (IOException | URISyntaxException e) {
                e.printStackTrace();
            }
        });
    }
}
