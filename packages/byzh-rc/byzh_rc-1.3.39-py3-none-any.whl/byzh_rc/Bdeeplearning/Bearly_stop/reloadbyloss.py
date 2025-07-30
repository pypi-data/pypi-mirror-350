class B_ReloadByLoss:
    def __init__(self, max_reload_count, reload_rounds, delta=0.01):
        '''
        连续reload_rounds次, val_loss - min_val_loss > delta, 则重新加载模型
        '''
        self.reload_rounds = reload_rounds
        self.delta = delta
        self.min_valLoss = float('inf')
        self.cnt_trigger = 0

        self.max_reload_count = max_reload_count
        self.cnt_reload = 0

        self.DONE = False
    def __call__(self, val_loss):
        if self.DONE:
            return 'normal'
        if val_loss >= self.min_valLoss + self.delta:
            self.cnt_trigger += 1
        if val_loss < self.min_valLoss:
            self.min_valLoss = val_loss
            self.cnt_trigger = 0
        if self.cnt_trigger > self.reload_rounds:
            self.cnt_reload += 1
            self.cnt_trigger = 0
            if self.cnt_reload == self.max_reload_count:
                self.DONE = True
            return 'reload'
        return 'normal'