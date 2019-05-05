class LearningState:
    def __init__(self, pre_cross_densities, global_aggregated_densities, phase_no, phase_duration):
        self.pre_cross_densities = pre_cross_densities
        self.global_aggregated_densities = global_aggregated_densities
        self.phase_no = phase_no
        self.phase_duration = phase_duration
    def __eq__(self, other):
        all_properties = [prop for prop in dir(self) if not prop.startswith('__')]
        for prop in all_properties:
            if getattr(self,prop)!=getattr(other,prop):
                return False
        return True
    def __hash__(self):
        all_properties = [prop for prop in dir(self) if not prop.startswith('__')]
        values = tuple([getattr(self,prop) for prop in all_properties])
        return hash(values)
