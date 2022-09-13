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
            <input type="text" name="threshold" class="form-control" v-model="threshold">
            <span class="input-group-text">%</span>
        </div>
        <input type="range" class="form-range" v-model="threshold">
        <button type="button" class="btn btn-success" @click="requestAnalysis"
            :disabled="filename == null && selectedModel == null">
            Analyze
        </button>
    </form>
    <div class="col-6" id="preview">
    </div>
</template>


<script>
export default {
    data() {
        return {
            threshold: 60,
            filename: null,
            selectedModel: null,
            models: [],
            preview: null
        }
    },
    mounted() {
        this.getModels();
        this.preview = document.querySelector("#preview");
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
                .then(classifications => {
                    console.log(classifications);
                    classifications.forEach((element, i) => {
                        const el = document.querySelector("#id-" + i);
                        console.log(element);
                        console.log(el);
                        if (element.confidence * 100 > this.threshold) {
                            el.style.color = "red";
                            console.log("Putting", el, "red");
                        }
                    });
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
.highlighted {
    color: red;
}
</style>