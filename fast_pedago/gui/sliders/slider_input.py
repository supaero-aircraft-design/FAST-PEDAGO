
import ipyvuetify as v
import traitlets


# TODO
# Implement tooltip
class SliderInput(v.VuetifyTemplate):
    min = traitlets.Float(default_value=0).tag(sync=True)
    max = traitlets.Float(default_value=100).tag(sync=True)
    step = traitlets.Float(default_value=10).tag(sync=True)
    label = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
    tooltip = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
    value = traitlets.Float(default_value=None, allow_none=True).tag(sync=True)
    
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
                    <v-slider
                        v-model="value"
                        class="align-center pe-3"
                        :max="max"
                        :min="min"
                        :step="step"
                        hide-details
                    >
                        <template v-slot:append>
                            <v-text-field
                                v-model="value"
                                class="mt-0 pt-0"
                                variant="outlined"
                                density="compact"
                                hide-details
                                single-line
                                type="number"
                                style="width: 60px"
                            >
                            </v-text-field>
                        </template>
                    </v-slider>
                </v-col>
            </v-row>
        </template>
        '''
