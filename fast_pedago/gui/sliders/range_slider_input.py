
import ipyvuetify as v
import traitlets

#TODO
# Implement tooltip
class RangeSliderInput(v.VuetifyTemplate):
    min = traitlets.Float(default_value=5).tag(sync=True)
    max = traitlets.Float(default_value=30).tag(sync=True)
    step = traitlets.Float(default_value=1).tag(sync=True)
    label = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
    tooltip = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
    range = traitlets.List(traitlets.Float(default_value=[10, 20], minlen=2, maxlen=2)).tag(sync=True)
    
    @traitlets.default('template')
    def _template(self):
        return f'''
        <template>
            <v-row
                justify="center"
            >
                <v-col
                    class="ps-8 pe-0 py-1"
                    cols=4
                >
                    <p>{self.label}</p>
                </v-col>

                <v-col
                    class="ps-3 py-1"
                >
                    <v-range-slider
                        v-model="range"
                        class="align-center pe-3"
                        :max="max"
                        :min="min"
                        :step="step"
                        hide-details
                    >
                        <template v-slot:prepend>
                            <v-text-field
                                :value="range[0]"
                                class="mt-0 pt-0"
                                density="compact"
                                style="width: 40px"
                                type="number"
                                variant="outlined"
                                hide-details
                                single-line
                            ></v-text-field>
                        </template>
                        
                        <template v-slot:append>
                            <v-text-field
                                :value="range[1]"
                                class="mt-0 pt-0"
                                density="compact"
                                style="width: 40px"
                                type="number"
                                variant="outlined"
                                hide-details
                                single-line
                            ></v-text-field>
                        </template>
                    </v-range-slider>
                </v-col>
            </v-row>
        </template>
        ''' 
