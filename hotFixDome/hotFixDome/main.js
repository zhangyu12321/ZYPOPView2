defineClass("ViewController", {
            
 viewWillAppear: function(animated) {
    self.super().viewWillAppear(animated);
            //balabala...
        },
viewWillDisappear: function(animated) {
    self.super().viewWillDisappear(animated);
            //balabala...
        },
  tableView_didSelectRowAtIndexPath: function(tableView, indexPath) {
    var row = indexPath.row()
    var cell = tableView.cellForRowAtIndexPath(indexPath);
    if (self.dataSource().length > row) {  //加上判断越界的逻辑
      var content = self.dataArr()[row];
      cell.textLabel().setText(content);
    }else{
      cell.textLabel().setText("zhangyu"); 
    }
  }
  
})
