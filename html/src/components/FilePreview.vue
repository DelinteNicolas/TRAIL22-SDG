<template>
    <main class="row">
        <form id="sidebarMenu" class="col-2">
            <div class="mb-1">
                <label for="formFile" class="form-label">Select a file</label>
                <input class="form-control" type="file" id="formFile" @change="uploadFile">
                </div>

            <div class="mb-1">
                <div v-for="model, i in models" :key="model" class="form-check">
                    <label class="form-check-label">
                        <input class="form-check-input" type="radio" name="modelRadio" :value="model"
                            @change="onModelSelectedChanged" :checked="i == 0">
                        {{model}}
                    </label>
                </div>
            </div>
            <div class="input-group mb-1">
                <label class="input-group-text" for="threshold">Detection threshold</label>
                <input type="number" name="threshold" class="form-control" v-model.number="threshold">
                <span class="input-group-text">%</span>
                </div>
            <input type="range" class="form-range" v-model.number="threshold">
            <button type="button" class="btn btn-success" @click="requestAnalysis"
                :disabled="pdf_filename == null || selectedModel == null">
                Analyze
                <i v-if="requesting" class="fa fa-spinner fa-spin"></i>
                <i v-else class="fa fa-play"></i>

            </button>
            </form>
            <div class="col-6 text-start text-wrap" ref="preview">
                <div class="text-center" v-if="pdf_filename == null">
                    Import a PDF to have a preview
                </div>
            </div>
            <StatsComponent :labels="labels" :colors="COLORS" :classifications="classifications" :threshold="threshold" />
            </main>
</template>


<script>
import { Tooltip } from "bootstrap";
import StatsComponent from "./StatsComponent.vue";

export default {
    data() {
        return {
            threshold: 60,
            selectedModel: null,
            models: [],
            classifications: [],
            labels: [],
            thresholdDebounce: null,
            pdf_filename: "",
            requesting: false,
            COLORS: ["#e16f78", "#e6c67b", "#72dd91", "#e1707d", "#e17669", "#78cce1", "#e2bf6e", "#e07391", "#e49971", "#e26cac", "#e5b270", "#e3b36b", "#86df73", "#6fbce2", "#70e47b", "#68aedc", "#7099de"]
        };
    },
    watch: {
        /**
         * Debounced watch of the threshold changes to update the interface.
         */
        threshold() {
            if (this.thresholdDebounce != null) {
                clearTimeout(this.thresholdDebounce);
            }
            this.thresholdDebounce = setTimeout(this.showClasses, 100);
        }
    },
    mounted() {
        this.getModels();
    },
    methods: {
        onModelSelectedChanged(event) {
            this.selectedModel = event.target.value;
        },
        getModels() {
            fetch("http://localhost:5000/models")
                .then(res => res.json())
                .then(model_list => {
                    this.models = model_list;
                    this.selectedModel = model_list[0];
                });
        },
        requestAnalysis() {
            this.requesting = true;
            fetch("http://localhost:5000/document/analyze", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    model: this.selectedModel,
                    filename: this.pdf_filename
                }),
            })
                .then(res => res.json())
                .then(json => {
                    this.classifications = json.classifications;
                    this.labels = json.labels;
                    this.showClasses();
                    this.requesting = false;
                });
        },
        showClasses() {
            this.classifications.forEach((element, i) => {
                const el = document.querySelector("#id-" + i);
                el.setAttribute("data-bs-toggle", "tooltip");
                el.setAttribute("data-bs-placement", "right");
                el.setAttribute("data-bs-title", "[" + Math.round(element.confidence * 100 * 100) / 100 + "%] SDG " + element.sdg + ": " + this.labels[element.label]);
                new Tooltip(el);
                if (element.confidence * 100 >= this.threshold) {
                    el.style.backgroundColor = this.COLORS[element.sdg];
                }
                else {
                    el.style.backgroundColor = null;
                }
            });
        },
        uploadFile(event) {
            const file = event.target.files[0];
            const formData = new FormData();
            formData.append("document", file);
            fetch("http://localhost:5000/document/upload", {
                method: "POST",
                body: formData,
                mode: "cors"
            })
                .then(res => res.json())
                .then(json => {
                    this.$refs.preview.innerHTML = json.html;
                    this.pdf_filename = json.filename;
                })
                .catch(err => console.error(err));
        }
    },
    components: { StatsComponent }
}
</script>

<style>
sentence {
    border-radius: 5%;
}
</style>