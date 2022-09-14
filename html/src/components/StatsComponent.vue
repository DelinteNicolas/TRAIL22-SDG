<template>
    <div class="col-4">
        <Doughnut ref="piechart" :chart-options="chartOptions" :chart-data="chartData" />
    </div>
</template>


<script>
import { Doughnut } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables);


export default {
    components: { Doughnut },
    data() {
        return {
            debouncedUpdate: null,
            chartOptions: {
                responsive: true
            }
        }
    },
    props: {
        colors: Array,
        classifications: Array,
        threshold: Number,
        labels: Array
    },
    watch: {
        threshold() {
            this.debouncedUpdatePlots();
        },
        classifications() {
            this.debouncedUpdatePlots();
        }
    },
    computed: {
        labelsHistogram() {
            const histo = new Array(this.nLabels + 1).fill(0);
            this.classifications.forEach(clf => {
                if (clf.confidence * 100 >= this.threshold) {
                    histo[clf.sdg]++;
                }
            });
            return histo;
        },
        nLabels() {
            return this.labels.length;
        },
        chartData() {
            const histo = this.labelsHistogram;
            console.log(histo);
            return {
                labels: this.labels,
                datasets: [{
                    label: 'Colours dataset',
                    data: histo,
                    backgroundColor: this.colors,
                    hoverOffset: 4
                }]
            };
        }
    },
    methods: {
        debouncedUpdatePlots() {
            if (this.debouncedUpdate == null) {
                clearTimeout(this.debouncedUpdate);
            }
            this.debouncedUpdate = setTimeout(this.updatePlots, 100);
        },
        updatePlots() {
            this.$refs.piechart.updateChart();
        }
    }
}
</script>