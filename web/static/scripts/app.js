// N'utiliser qu'une seul vue par fichier, éviter les Vue multiple
const app_vue = new Vue({
    el: '#app',
    data: {
        co2_rate_all_data: [],
        co2_rate_all_data_last_n: [],
        numb_values_to_display: 20,
        chart: "",
    },
    methods: {
        fetch_elements() {
            let self = this;
            let get_url = "api/Get_Co2_Rate_Data/"
            axios.get(get_url, {}
            ).then(function (response) {
                self.co2_rate_all_data = response.data;
                self.co2_rate_all_data_last_n = self.co2_rate_all_data.slice(-self.numb_values_to_display);
                self.extract_and_display_data_bar_chart(self.co2_rate_all_data_last_n)
                console.log('SUCCESS!!');
            }).catch(function (response) {
                console.error(JSON.stringify(response.message));
                console.log('FAILURE!!');
            });
        },

        extract_and_display_data_bar_chart(co2_rate_all_data_last_n) {
            let labels = [];
            let colors = [];
            let diffs = [];
            let used_colors= ["#0eafd2","#d20e2b"]
            co2_rate_all_data_last_n.forEach((data) => {
                labels.push(data.dt);
                let diff = data.dif;
                if (diff >= 0) {
                    colors.push(used_colors[0])
                } else {
                    colors.push(used_colors[1])
                }
                diffs.push(diff)
            });
            this.display_chart_bar(labels, diffs, colors,used_colors);
        },
        display_chart_bar(labels, diffs, colors, used_colors) {
            const ctx = $('#co2_chart_bar').get(0).getContext('2d');
            if (this.chart) {
                this.chart.destroy()
            }
            this.chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Difference",
                        backgroundColor: colors,
                        data: diffs,
                        colors:used_colors
                    }]
                },
                options: options_bar_chart
            });
            $("#legend").html(this.chart.generateLegend())
        }

    },
    watch: {
        numb_values_to_display: function (val) {
            if (val > 0) {
                this.co2_rate_all_data_last_n = this.co2_rate_all_data.slice(-val);
                this.extract_and_display_data_bar_chart(this.co2_rate_all_data_last_n)
            }
        }
    },
    delimiters: ["<%", "%>"]
});

const options_bar_chart = {
    title: {
        display: true,
        text: 'Co2 Rate en fonction de la date',
        position: 'top',

    },
    responsive: true,
    legend: false,
    // maintainAspectRatio: false,
    legendCallback: function (chart) {
        const text = [];
        text.push('<ul class="' + chart.id + '_legend">');

        text.push('<li><span style="background-color:' + chart.data.datasets[0].colors[0] + '"></span>');
        text.push('<span class="legend_label">Difference positive</span>');
        text.push('</li>');

        text.push('<li><span style="background-color:' + chart.data.datasets[0].colors[1] + '"></span>');
        text.push('<span class="legend_label">Difference negative</span>');
        text.push('</li>');
        // }
        text.push('</ul>');
        return text.join("");
    }
};
