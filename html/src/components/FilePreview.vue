<template>
    <form id="sidebarMenu" class="col-2" @drop="onDrop">
        <div class="mb-1">
            <label for="formFile" class="form-label">Default file input example</label>
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
            <input type="number" name="threshold" class="form-control" v-model="threshold">
            <span class="input-group-text">%</span>
        </div>
        <input type="range" class="form-range" v-model="threshold">
        <button type="button" class="btn btn-success" @click="requestAnalysis"
            :disabled="filename == null && selectedModel == null">
            Analyze
        </button>
    </form>
    <div class="col-6 text-start text-wrap" id="preview">
    </div>
</template>


<script>
import { Tooltip } from "bootstrap";
export default {
    data() {
        return {
            threshold: 60,
            filename: null,
            selectedModel: null,
            models: [],
            preview: null,
            classifications: [],
            labels: [],
            thresholdDebounce: null
        }
    },
    watch: {
        threshold() {
            if (this.thresholdDebounce != null) {
                clearTimeout(this.thresholdDebounce);
            }
            this.thresholdDebounce = setTimeout(this.showClasses, 100);
        }
    },
    mounted() {
        this.getModels();
        this.preview = document.querySelector("#preview");
    },
    computed: {
        fileData() {
            const file = document.querySelector("#formFile").files[0];
            const formData = new FormData();
            formData.append("document", file);
            return formData;
        }
    },  
    methods: {
        onModelSelectedChanged(event) {
            this.selectedModel = event.target.value;
        },
        getModels() {
            fetch("http://localhost:5000/models")
                .then(res => res.json())
                .then(model_list => {
                    console.log(model_list);
                    this.models = model_list;
                    this.selectedModel = model_list[0];
                });
        },
        requestAnalysis(event) {
            console.log(event);
            fetch("http://localhost:5000/document/analyze", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: this.selectedModel,
                    filename: this.filename
                }),
            })
                .then(res => res.json())
                .then(json => {
                    console.log(json);
                    this.classifications = json.classifications;
                    this.labels = json.labels;
                    this.showClasses();
                });
        },
        showClasses() {
            this.classifications.forEach((element, i) => {
                const el = document.querySelector("#id-" + i);
                el.setAttribute("data-bs-toggle", "tooltip");
                el.setAttribute("data-bs-placement", "right");
                el.setAttribute("data-bs-title", "[" + Math.round(element.confidence * 100 * 100) / 100 + "%] SDG " + element.sdg + ": " + this.labels[element.label]);
                if (element.confidence * 100 >= this.threshold) {
                    el.classList.add("sdg" + element.sdg);
                } else {
                    el.classList.remove("sdg" + element.sdg);
                }
            });
            document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(element => {
                new Tooltip(element);
            }); 
            console.log("Done!");
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
                .then(res => {
                    console.log(res);
                    this.preview.innerHTML = res.html;
                    this.filename = res.filename;
                });
        }
    }
}
</script>

<style>
.sdg1 {
    background-color: #e16f78;
}

.sdg2 {
    background-color: #e6c67b;
}

.sdg3 {
    background-color: #e6c67b;
}

.sdg4 {
    background-color: #e1707d;
}

.sdg5 {
    background-color: #e17669;
}

.sdg6 {
    background-color: #78cce1;
}

.sdg7 {
    background-color: #e2bf6e;
}

.sdg8 {
    background-color: #e07391;
}

.sdg9 {
    background-color: #e49971;
}

.sdg10 {
    background-color: #e26cac;
}

.sdg11 {
    background-color: #e5b270;
}

.sdg12 {
    background-color: #e3b36b;
}

.sdg13 {
    background-color: #86df73;
}

.sdg14 {
    background-color: #6fbce2;
}

.sdg15 {
    background-color: #70e47b;
}

.sdg16 {
    background-color: #68aedc;
}

.sdg17 {
    background-color: #7099de;
}
</style>