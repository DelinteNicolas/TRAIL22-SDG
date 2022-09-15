<template>
    <div class="col-4">
        <Doughnut ref="piechart" :chart-data="chartData" />
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
    computed: {
        nLabels() {
            return this.labels.length;
        },
        chartData() {
            const histo = this.labelsHistogram();
            return {
                labels: this.labels,
                datasets: [{
                    label: "Colours dataset",
                    data: histo,
                    backgroundColor: this.colors,
                    hoverOffset: 4
                }]
            };
        }
    },
    methods: {
        labelsHistogram() {
            const histo = new Array(this.nLabels + 1).fill(0);
            this.classifications.forEach(clf => {
                if (clf.confidence * 100 >= this.threshold) {
                    histo[clf.sdg]++;
                }
            });
            return histo;
        },
    }
}
</script>