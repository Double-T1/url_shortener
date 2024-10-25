import { library, dom } from "@fortawesome/fontawesome-svg-core";

import { faCloudArrowDown } from "@fortawesome/free-solid-svg-icons";
import { faCopy, faCircleCheck, faCircleXmark } from "@fortawesome/free-regular-svg-icons";


library.add( faCloudArrowDown, faCopy, faCircleCheck, faCircleXmark );

dom.i2svg();
dom.watch();